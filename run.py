from analyst_agent import run_agent

if __name__ == "__main__":
    final_state = run_agent(
        task="Analyze the pros and cons of local vs cloud LLMs"
    )

    print("FINAL OUTPUT:")
    print(final_state.final_output)