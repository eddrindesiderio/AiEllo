#!/usr/bin/env python3
"""
AI Agent Builder - Create Autonomous AI Agents
This demonstrates how to build AI agents that can perform tasks autonomously.

AI Agents can:
- Break down complex tasks into steps
- Use tools and APIs
- Make decisions and take actions
- Learn from feedback and improve

This code shows how AI can help you build more advanced AI systems!
"""

import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any, Optional

load_dotenv()

class AIAgent:
    """
    An autonomous AI agent that can think, plan, and execute tasks.
    Built with AI assistance to demonstrate AI building AI!
    """
    
    def __init__(self, name: str, role: str, capabilities: List[str] = None):
        self.name = name
        self.role = role
        self.capabilities = capabilities or []
        self.memory = []
        self.tools = {}
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if self.api_key:
            openai.api_key = self.api_key
        
        # Register built-in tools
        self.register_tool("web_search", self.web_search)
        self.register_tool("file_operations", self.file_operations)
        self.register_tool("code_execution", self.code_execution)
        self.register_tool("memory_operations", self.memory_operations)
        
        print(f"🤖 AI Agent '{name}' initialized!")
        print(f"   Role: {role}")
        print(f"   Capabilities: {', '.join(capabilities)}")
        print(f"   Available tools: {', '.join(self.tools.keys())}")
    
    def register_tool(self, name: str, function):
        """Register a tool that the agent can use"""
        self.tools[name] = function
        print(f"🔧 Registered tool: {name}")
    
    def think(self, task: str) -> Dict[str, Any]:
        """
        Agent thinks about a task and creates a plan
        This uses AI to help the AI agent plan!
        """
        if not self.api_key or self.api_key == "your-openai-api-key-here":
            return {
                "plan": ["Cannot create plan - no API key available"],
                "reasoning": "Need OpenAI API key to enable thinking capabilities",
                "tools_needed": [],
                "confidence": 0.0
            }
        
        thinking_prompt = f"""
        You are {self.name}, an AI agent with the role: {self.role}
        
        Your capabilities: {', '.join(self.capabilities)}
        Available tools: {', '.join(self.tools.keys())}
        
        Task: {task}
        
        Think step by step and create a plan to accomplish this task.
        
        Respond in JSON format:
        {{
            "plan": ["step 1", "step 2", "step 3"],
            "reasoning": "why this approach will work",
            "tools_needed": ["tool1", "tool2"],
            "confidence": 0.8
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI agent planning system. Always respond with valid JSON."},
                    {"role": "user", "content": thinking_prompt}
                ],
                temperature=0.3
            )
            
            plan_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                plan = json.loads(plan_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                plan = {
                    "plan": [f"Analyze task: {task}", "Break down into steps", "Execute systematically"],
                    "reasoning": "Using fallback planning approach",
                    "tools_needed": ["general_reasoning"],
                    "confidence": 0.5
                }
            
            # Store in memory
            self.memory.append({
                "type": "planning",
                "task": task,
                "plan": plan,
                "timestamp": datetime.now().isoformat()
            })
            
            return plan
            
        except Exception as e:
            return {
                "plan": [f"Error in planning: {str(e)}"],
                "reasoning": "Planning system encountered an error",
                "tools_needed": [],
                "confidence": 0.0
            }
    
    def execute_plan(self, plan: Dict[str, Any], task: str) -> Dict[str, Any]:
        """Execute the planned steps"""
        print(f"\n🚀 {self.name} executing plan for: {task}")
        print(f"📋 Plan confidence: {plan.get('confidence', 0):.1%}")
        
        results = []
        
        for i, step in enumerate(plan.get('plan', []), 1):
            print(f"\n📍 Step {i}: {step}")
            
            # Simulate step execution
            step_result = self.execute_step(step, plan.get('tools_needed', []))
            results.append({
                "step": step,
                "result": step_result,
                "timestamp": datetime.now().isoformat()
            })
            
            # Brief pause to simulate processing
            time.sleep(0.5)
        
        execution_result = {
            "task": task,
            "plan": plan,
            "results": results,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }
        
        # Store in memory
        self.memory.append({
            "type": "execution",
            "data": execution_result
        })
        
        return execution_result
    
    def execute_step(self, step: str, tools_needed: List[str]) -> str:
        """Execute a single step of the plan"""
        # This is where the agent would actually perform actions
        # For demo purposes, we'll simulate different types of actions
        
        step_lower = step.lower()
        
        if "search" in step_lower or "research" in step_lower:
            return self.web_search(step)
        elif "file" in step_lower or "save" in step_lower:
            return self.file_operations(step)
        elif "code" in step_lower or "program" in step_lower:
            return self.code_execution(step)
        elif "remember" in step_lower or "memory" in step_lower:
            return self.memory_operations(step)
        else:
            return f"✅ Completed: {step}"
    
    def web_search(self, query: str) -> str:
        """Simulate web search capability"""
        return f"🔍 Searched for: {query} (simulated - would use real search API)"
    
    def file_operations(self, operation: str) -> str:
        """Handle file operations"""
        return f"📁 File operation: {operation} (simulated)"
    
    def code_execution(self, code_task: str) -> str:
        """Handle code-related tasks"""
        return f"💻 Code task: {code_task} (simulated)"
    
    def memory_operations(self, memory_task: str) -> str:
        """Handle memory operations"""
        memory_count = len(self.memory)
        return f"🧠 Memory operation: {memory_task} (Current memory items: {memory_count})"
    
    def reflect(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """Agent reflects on its performance and learns"""
        if not self.api_key or self.api_key == "your-openai-api-key-here":
            return {"reflection": "Cannot reflect without API key", "improvements": []}
        
        reflection_prompt = f"""
        You are {self.name}, reflecting on a completed task.
        
        Task: {execution_result['task']}
        Plan confidence: {execution_result['plan'].get('confidence', 0)}
        Steps executed: {len(execution_result['results'])}
        
        Results: {json.dumps(execution_result['results'], indent=2)}
        
        Reflect on:
        1. What went well?
        2. What could be improved?
        3. What did you learn?
        4. How would you approach this differently next time?
        
        Respond in JSON format:
        {{
            "reflection": "overall assessment",
            "improvements": ["improvement 1", "improvement 2"],
            "lessons_learned": ["lesson 1", "lesson 2"],
            "confidence_adjustment": 0.1
        }}
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a reflective AI agent. Always respond with valid JSON."},
                    {"role": "user", "content": reflection_prompt}
                ],
                temperature=0.4
            )
            
            reflection_text = response.choices[0].message.content
            reflection = json.loads(reflection_text)
            
            # Store reflection in memory
            self.memory.append({
                "type": "reflection",
                "data": reflection,
                "timestamp": datetime.now().isoformat()
            })
            
            return reflection
            
        except Exception as e:
            return {
                "reflection": f"Reflection error: {str(e)}",
                "improvements": ["Fix reflection system"],
                "lessons_learned": ["Error handling is important"],
                "confidence_adjustment": 0.0
            }
    
    def run_autonomous_task(self, task: str) -> Dict[str, Any]:
        """Run a complete autonomous task cycle"""
        print(f"\n🎯 {self.name} starting autonomous task: {task}")
        print("=" * 60)
        
        # Think and plan
        print("🤔 Thinking and planning...")
        plan = self.think(task)
        
        print(f"\n📋 Plan created:")
        print(f"   Reasoning: {plan.get('reasoning', 'N/A')}")
        print(f"   Confidence: {plan.get('confidence', 0):.1%}")
        print(f"   Steps: {len(plan.get('plan', []))}")
        
        # Execute plan
        execution_result = self.execute_plan(plan, task)
        
        # Reflect on results
        print(f"\n🤔 Reflecting on performance...")
        reflection = self.reflect(execution_result)
        
        print(f"\n💭 Reflection:")
        print(f"   Assessment: {reflection.get('reflection', 'N/A')}")
        print(f"   Improvements: {len(reflection.get('improvements', []))}")
        
        # Complete result
        complete_result = {
            "agent": self.name,
            "task": task,
            "plan": plan,
            "execution": execution_result,
            "reflection": reflection,
            "timestamp": datetime.now().isoformat()
        }
        
        return complete_result
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of the agent's memory"""
        memory_types = {}
        for item in self.memory:
            item_type = item.get('type', 'unknown')
            memory_types[item_type] = memory_types.get(item_type, 0) + 1
        
        return {
            "total_memories": len(self.memory),
            "memory_types": memory_types,
            "recent_memories": self.memory[-5:] if self.memory else []
        }

def create_example_agents():
    """Create some example AI agents"""
    agents = []
    
    # Research Agent
    research_agent = AIAgent(
        name="ResearchBot",
        role="Research and Information Gathering Specialist",
        capabilities=["web_search", "data_analysis", "report_generation"]
    )
    agents.append(research_agent)
    
    # Code Agent
    code_agent = AIAgent(
        name="CodeMaster",
        role="Software Development Assistant",
        capabilities=["code_generation", "debugging", "testing", "documentation"]
    )
    agents.append(code_agent)
    
    # Creative Agent
    creative_agent = AIAgent(
        name="CreativeGenius",
        role="Creative Content and Idea Generator",
        capabilities=["brainstorming", "content_creation", "design_thinking"]
    )
    agents.append(creative_agent)
    
    return agents

def demonstrate_ai_agents():
    """Demonstrate AI agents in action"""
    print("""
    🤖 AI Agent Builder Demo
    
    This shows how you can use AI to build autonomous AI agents.
    These agents can:
    - Think and plan autonomously
    - Use tools and capabilities
    - Learn from experience
    - Reflect and improve
    
    Let's see them in action!
    """)
    
    # Create example agents
    agents = create_example_agents()
    
    # Example tasks
    tasks = [
        "Research the latest trends in AI development",
        "Create a simple Python script for data analysis",
        "Brainstorm ideas for a mobile app"
    ]
    
    print(f"\n🎯 Running {len(tasks)} tasks across {len(agents)} agents...")
    
    results = []
    
    for i, (agent, task) in enumerate(zip(agents, tasks)):
        print(f"\n{'='*80}")
        print(f"🤖 Agent {i+1}/{len(agents)}: {agent.name}")
        print(f"📋 Task: {task}")
        
        result = agent.run_autonomous_task(task)
        results.append(result)
        
        # Show memory summary
        memory_summary = agent.get_memory_summary()
        print(f"\n🧠 Memory Summary: {memory_summary['total_memories']} items")
        
        time.sleep(1)  # Brief pause between agents
    
    return results

def main():
    """Main function"""
    print("""
    🚀 Welcome to AI Agent Builder!
    
    This demonstrates how to create autonomous AI agents using AI assistance.
    
    Key concepts:
    • AI agents that can think, plan, and execute
    • Tool usage and capability systems
    • Memory and learning mechanisms
    • Reflection and self-improvement
    
    This entire system was designed with AI assistance, showing how
    AI can help you build more advanced AI systems!
    """)
    
    choice = input("\nRun agent demonstration? (y/n): ").strip().lower()
    
    if choice == 'y':
        results = demonstrate_ai_agents()
        
        print(f"\n🎉 Demonstration complete!")
        print(f"   Tasks completed: {len(results)}")
        print(f"   Agents used: {len(set(r['agent'] for r in results))}")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/agent_demo_{timestamp}.json"
        
        os.makedirs("logs", exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"   Results saved to: {filename}")
        
    else:
        print("\n🤖 You can also create your own agents:")
        print("   agent = AIAgent('MyBot', 'Custom Role', ['capability1', 'capability2'])")
        print("   result = agent.run_autonomous_task('Your task here')")
        print("\n💡 Pro tip: Ask AI to help you design custom agents for your specific needs!")

if __name__ == "__main__":
    main()
