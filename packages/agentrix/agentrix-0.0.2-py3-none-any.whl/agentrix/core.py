import json
import concurrent.futures  # For parallel execution

# Define tool functions
class Tool:
    def __init__(self, name, description, function, inputs=None):
        self.name = name
        self.description = description
        self.function = function
        # Convert inputs to OpenAI function parameters format
        self.parameters = self._build_parameters(inputs or {})
    
    def _build_parameters(self, inputs):
        """Build parameters with configurable types"""
        properties = {}
        for name, config in inputs.items():
            if isinstance(config, list):
                # Format: [type, description]
                param_type, description = config
                properties[name] = {
                    "type": param_type,
                    "description": description
                }
            elif isinstance(config, dict):
                # Format: {"type": "string", "description": "desc", ...}
                properties[name] = config
            else:
                # Default string type for backward compatibility
                properties[name] = {
                    "type": "string",
                    "description": config
                }
        
        return {
            "type": "object",
            "properties": properties,
            "required": list(inputs.keys())
        }
    
    def execute(self, **kwargs):
        return self.function(**kwargs)

class Agent:
    def __init__(self, name, system_prompt, llm, model_name="gpt-4o", tools=None, verbose=False):
        self.name = name
        self.system_prompt = system_prompt
        self.model_name = model_name
        self.tools = tools or []
        self.conversation_history = []
        self.client = llm
        self.is_manager = False
        self.verbose = verbose  # Add verbose flag
    
    def add_tool(self, tools):
        """Add one or more tools to the agent"""
        if isinstance(tools, list):
            self.tools.extend(tools)
        else:
            self.tools.append(tools)
    
    def get_tools_config(self):
        return [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
        } for tool in self.tools]
    
    def go(self, input_message):
        if self.verbose:
            print(f"\n🤖 [{self.name}] Processing: {input_message}")
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_message}
            ],
            tools=self.get_tools_config(),
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                for tool in self.tools:
                    if tool.name == tool_call.function.name:
                        if self.verbose:
                            print(f"🔧 [{self.name}] Using tool: {tool.name}")
                        
                        arguments = json.loads(tool_call.function.arguments)
                        result = tool.execute(**arguments)
                        
                        if not self.is_manager:
                            if self.verbose:
                                print(f"✓ [{self.name}] Result: {result}")
                            return result
                        
                        # For manager, return natural summary
                        final_response = self.client.chat.completions.create(
                            model=self.model_name,
                            messages=[
                                {"role": "system", "content": "Summarize this information naturally:"},
                                {"role": "user", "content": result}
                            ]
                        )
                        return final_response.choices[0].message.content
        
        return assistant_message.content or "I couldn't generate a response."

class ManagerAgent(Agent):
    """
    A manager agent that treats other agents as tools.
    Each agent becomes available as a tool that the manager can call.
    """
    def __init__(self, name, system_prompt, llm, model_name="gpt-4o", agents=None, parallel=False, verbose=False):
        super().__init__(name, system_prompt, llm, model_name, verbose=verbose)
        self.agent_tools = []
        self.is_manager = True
        self.parallel = parallel  # Add parallel execution flag
        if agents:
            self.register_agents([agent[0] for agent in agents], 
                               {agent[0].name: agent[1] for agent in agents})
    
    def register_agent(self, agent, description=None):
        if description is None:
            description = f"Use the {agent.name} for tasks related to its expertise"
        
        def call_agent(query):
            result = agent.go(query)
            # Remove the prefix if present
            return result.replace(f"[{agent.name}]: ", "") if isinstance(result, str) else result
        
        # Create a tool for this agent
        agent_tool = Tool(
            name=agent.name,
            description=description,
            function=call_agent,
            inputs={"query": f"The question or task to ask the {agent.name}"}
        )
        
        self.add_tool(agent_tool)
        self.agent_tools.append(agent_tool)
        return self
        
    def register_agents(self, agents, descriptions=None):
        """
        Register multiple agents at once
        """
        if descriptions is None:
            descriptions = {}
            
        for agent in agents:
            self.register_agent(agent, descriptions.get(agent.name))
            
        return self
    
    def go(self, input_message):
        # First, analyze the input to identify if there are multiple queries
        planning_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system", 
                    "content": f"""You are the planning stage of a manager agent.
Your job is to analyze the user query and determine if it contains multiple distinct requests 
that should be handled by different specialized agents. If so, break down the query into 
separate tasks. For each task, identify which agent ({', '.join([tool.name for tool in self.agent_tools])}) 
should handle it and what specific question should be asked to that agent."""
                },
                {"role": "user", "content": input_message}
            ]
        )
        
        planning_result = planning_response.choices[0].message.content
        
        # Now pass the input to the LLM for actual processing
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_message},
                {"role": "assistant", "content": "I'll analyze this request and provide a comprehensive response using the appropriate specialized agents."},
                {"role": "user", "content": f"Planning analysis: {planning_result}\n\nPlease process this request using the appropriate agents. If multiple agents are needed, use them efficiently."}
            ],
            tools=self.get_tools_config(),
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        if assistant_message.tool_calls:
            # Handle parallel execution if enabled
            if self.parallel and len(assistant_message.tool_calls) > 1:
                return self._execute_parallel(assistant_message.tool_calls, input_message)
            else:
                # Sequential execution (original behavior)
                return self._execute_sequential(assistant_message.tool_calls, input_message)
        
        return assistant_message.content or "I couldn't generate a response."
    
    def _execute_sequential(self, tool_calls, original_query):
        """Execute tool calls sequentially (original behavior)"""
        results = []
        
        for tool_call in tool_calls:
            for tool in self.tools:
                if tool.name == tool_call.function.name:
                    arguments = json.loads(tool_call.function.arguments)
                    result = tool.execute(**arguments)
                    # Include agent name with result for better context
                    results.append(f"[{tool.name}]: {result}")
        
        # Combine results
        combined_result = "\n\n".join(results)
        
        # Generate natural summary of the combined results
        final_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system", 
                    "content": "Synthesize the information from multiple agents into a cohesive response that addresses all parts of the user's original query."
                },
                {"role": "user", "content": f"Original query: {original_query}\n\nAgent responses:\n{combined_result}"}
            ]
        )
        
        return final_response.choices[0].message.content
    
    def _execute_parallel(self, tool_calls, original_query):
        """Execute tool calls in parallel using ThreadPoolExecutor"""
        tasks = []
        tool_names = []
        
        # Prepare all tasks
        print("\n=== Starting Parallel Execution ===")
        for tool_call in tool_calls:
            for tool in self.tools:
                if tool.name == tool_call.function.name:
                    arguments = json.loads(tool_call.function.arguments)
                    tasks.append((tool, arguments))
                    tool_names.append(tool.name)
                    print(f"✓ Prepared task for: {tool.name}")
        
        results = []
        
        # Execute tasks in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            print("\n=== Executing Tasks in Parallel ===")
            futures = []
            for task, args in tasks:
                future = executor.submit(task.execute, **args)
                futures.append((future, task.name))
                print(f"▶ Started: {task.name}")
            
            # Wait for completion
            for future, name in futures:
                try:
                    result = future.result()
                    print(f"✓ Completed: {name}")
                    results.append(f"[{name}]: {result}")
                except Exception as e:
                    print(f"✗ Failed: {name} - {str(e)}")
                    results.append(f"[{name}] Error: {str(e)}")
        
        print("\n=== All Tasks Completed ===")
        return self._summarize_results(results, original_query)

    def _summarize_results(self, results, original_query):
        """Summarize results from parallel execution"""
        combined_result = "\n".join(results)
        
        final_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system", 
                    "content": "Synthesize the information from multiple agents into a cohesive response."
                },
                {"role": "user", "content": f"Original query: {original_query}\n\nAgent responses:\n{combined_result}"}
            ]
        )
        
        return final_response.choices[0].message.content

