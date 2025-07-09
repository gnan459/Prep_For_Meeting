from textwrap import dedent
from crewai import Agent
from llm import llm
from tools.ExaSearchTool import get_exa_tools
from tools.SerperSearchTool import get_serper_tools

class MeetingPreparationAgents():
	def research_agent(self):
		return Agent(
			role='Research Specialist',
			goal='Conduct thorough research on people and companies involved in the meeting',
			tools=get_serper_tools(),
			llm=llm,
			backstory=dedent("""\
					 As a Research Specialist, your mission is to uncover detailed information
                about the individuals and entities participating in the meeting. Your insights
                will lay the groundwork for strategic meeting preparation.

                Prioritize data from LinkedIn such as About, Experience, and Education sections.
                If full profiles aren't available, use your knowledge to generate educated summaries.."""),
			verbose=True
		)

	def industry_analysis_agent(self):
		return Agent(
			role='Industry Analyst',
			goal='Analyze the current industry trends, challenges, and opportunities',
			tools=get_exa_tools(),
			llm=llm,
			backstory=dedent("""\
					As an Industry Analyst, your analysis will identify key trends,
					challenges facing the industry, and potential opportunities that
					could be leveraged during the meeting for strategic advantage."""),
			verbose=True
		)

	def meeting_strategy_agent(self):
		return Agent(
			role='Meeting Strategy Advisor',
			goal='Develop talking points, questions, and strategic angles for the meeting',
			tools=get_exa_tools(),
			llm=llm,
			backstory=dedent("""\
					As a Strategy Advisor, your expertise will guide the development of
					talking points, insightful questions, and strategic angles
					to ensure the meeting's objectives are achieved."""),
			verbose=True
		)

	def summary_and_briefing_agent(self):
		return Agent(
			role='Briefing Coordinator',
			goal='Compile a 5-part structured summary for the meeting',
			tools=get_exa_tools(),
			llm=llm,
			backstory=dedent("""\
				You are responsible for writing the final output.
				Combine the findings from the other agents into a clear, well-structured
				briefing document with sections like Executive Summary, Bios, Trends, Talking Points,
				and Strategic Recommendations.
			"""),
			verbose=True
		)
