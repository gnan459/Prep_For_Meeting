from textwrap import dedent
from crewai import Task

class MeetingPreparationTasks():
    def research_task(self, agent, participants, context):
        return Task(
            description=dedent(f"""
                Use the SerperSearch tool to find LinkedIn profiles for the following participants:
                {participants}

                For each participant:
                - Search using: "LinkedIn <participant_name>"
                - Ensure the query includes: `site:linkedin.com/in`
                - Only return structured output from the search results. Do not summarize or infer content.
                - Your job is to extract:
                  • Name
                  • Top 1–2 snippet summaries (if present)
                  • LinkedIn profile URL (if available)
                - Do NOT fabricate or guess URLs. Only return LinkedIn links that appear in search results.
                Return the results exactly as found in the search JSON.
            """),
            expected_output=dedent("""
                Output JSON format:
                [
                  {
                    "name": "Participant Name",
                    "linkedin_url": "<URL or null>",
                    "snippets": ["Snippet 1", "Snippet 2"]
                  },
                  ...
                ]
            """),
            async_execution=False,  # Can be done in parallel
            agent=agent,
            output_json=True
        )

    def industry_analysis_task(self, agent, participants, context):
        return Task(
            description=dedent(f"""\
                Analyze the current industry trends, challenges, and opportunities
                relevant to the meeting's context. Consider market reports, recent
                developments, and expert opinions to provide a comprehensive overview
                of the industry landscape.

                Participants: {participants}
                Meeting Context: {context}
            """),
            expected_output=dedent("""\
                An insightful analysis that identifies major trends, potential
                challenges, and strategic opportunities.
            """),
            async_execution=False,  # Can also run in parallel
            agent=agent,
            output_json=True
        )

    def meeting_strategy_task(self, agent, context, objective):
        return Task(
            description=dedent(f"""\
                Develop strategic talking points, questions, and discussion angles
                for the meeting based on the research and industry analysis conducted.

                Meeting Context: {context}
                Meeting Objective: {objective}
            """),
            expected_output=dedent("""\
                A complete report with key talking points, strategic questions,
                and proposed angles to achieve the meeting's objective.
            """),
            async_execution=False,  # Depends on prior tasks
            agent=agent,
            output_json=True
        )

    def summary_and_briefing_task(self, agent, context, objective):
        return Task(
            description=dedent(f"""\
                Compile all the research findings, industry analysis, and strategic
                talking points into a concise, comprehensive briefing document for
                the meeting. Ensure the briefing is easy to digest and equips
                participants with all necessary information and strategies.
                               
                If the Participant Bios contain only snippets and a LinkedIn URL, 
                do NOT generate summaries or descriptions. Only list the name, the snippet, and the LinkedIn URL.

                Meeting Context: {context}
                Meeting Objective: {objective}
            """),
            expected_output=dedent("""\
            A well-structured briefing document that includes:
            - Participant bios (based on retrieved LinkedIn URLs and snippets)
            - Industry overview
            - Talking points
            - Strategic recommendations
            """),
            async_execution=False,  # Should run last
            agent=agent,
            output_json=True
        )
