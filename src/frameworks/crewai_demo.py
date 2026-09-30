from crewai import Agent, Crew, Process, Task


def build_crew():
    researcher = Agent(
        role="Market Researcher",
        goal="Identify relevant financial market evidence.",
        backstory=(
            "You are a financial research specialist "
            "who gathers factual market evidence."
        ),
        verbose=False,
    )

    analyst = Agent(
        role="Market Analyst",
        goal="Analyze the evidence provided by the researcher.",
        backstory=(
            "You analyze market and financial-news evidence "
            "without making autonomous trading decisions."
        ),
        verbose=False,
    )

    reviewer = Agent(
        role="Evidence Reviewer",
        goal="Check whether sufficient evidence exists.",
        backstory=(
            "You review financial analysis for evidence completeness "
            "and identify when more research is required."
        ),
        verbose=False,
    )

    research_task = Task(
        description=(
            "Describe what market and financial-news evidence "
            "should be collected for a stock analysis."
        ),
        expected_output=(
            "A concise list of required market and financial-news evidence."
        ),
        agent=researcher,
    )

    analysis_task = Task(
        description=(
            "Explain how the collected evidence should be analyzed "
            "for a market-intelligence report."
        ),
        expected_output="A concise evidence-based analysis approach.",
        agent=analyst,
    )

    review_task = Task(
        description=(
            "Define the conditions under which the evidence should "
            "be considered sufficient for review approval."
        ),
        expected_output="A concise evidence sufficiency assessment.",
        agent=reviewer,
    )

    return Crew(
        agents=[researcher, analyst, reviewer],
        tasks=[research_task, analysis_task, review_task],
        process=Process.sequential,
        verbose=False,
    )


if __name__ == "__main__":
    crew = build_crew()

    print("CrewAI demonstration configured successfully.")
    print("Agents: Researcher -> Analyst -> Reviewer")
    print("Process: sequential")