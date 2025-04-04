# RS Copilot Prompts

This document contains examples of RS Copilot prompts that can be used with GitHub Copilot or Edge Copilot to optimize code. These prompts help guide the AI to produce better code optimizations.

## Long Function Optimization Prompt

Use this prompt to help split long functions into subfunctions before optimizing:

```
I have a long function that needs to be optimized. Please help me refactor it by:

1. Identifying logical sections that could be extracted into separate functions
2. Creating well-named helper functions with clear responsibilities
3. Maintaining the same functionality while improving:
   - Readability
   - Maintainability
   - Testability
4. Adding appropriate error handling
5. Ensuring proper documentation for each function

Here's the function:

[PASTE YOUR FUNCTION HERE]
```

## Modularized Optimization Prompt

Use this prompt if you have spaghetti code and want to modularize it into functions before optimizing:

```
I need to modularize this code into well-structured functions. Please help me by:

1. Identifying distinct responsibilities in the code
2. Creating separate functions for each responsibility
3. Organizing the functions in a logical way
4. Ensuring proper parameter passing between functions
5. Adding appropriate error handling
6. Including clear documentation for each function

Here's the code:

[PASTE YOUR CODE HERE]
```

## Code Review Optimization Prompt

Use this prompt to get optimization suggestions for your code:

```
Please review this code and suggest optimizations for:

1. Performance improvements
2. Better error handling
3. More efficient algorithms or data structures
4. Improved readability and maintainability
5. Potential bugs or edge cases
6. Following best practices for [LANGUAGE/FRAMEWORK]

Here's the code:

[PASTE YOUR CODE HERE]
```

## Function Signature Optimization Prompt

Use this prompt to improve function signatures:

```
I want to improve the function signatures in this code. Please help me by:

1. Identifying functions with unclear or overly complex signatures
2. Suggesting better parameter names and ordering
3. Recommending appropriate default values
4. Adding type hints/annotations where applicable
5. Considering whether parameters should be grouped into objects
6. Ensuring return values are clear and consistent

Here's the code:

[PASTE YOUR CODE HERE]
```

## Documentation Optimization Prompt

Use this prompt to improve code documentation:

```
Please help me improve the documentation for this code by:

1. Adding clear function/method docstrings
2. Documenting parameters and return values
3. Explaining complex logic or algorithms
4. Adding examples of usage where helpful
5. Ensuring consistency in documentation style
6. Following documentation best practices for [LANGUAGE/FRAMEWORK]

Here's the code:

[PASTE YOUR CODE HERE]
```

## Error Handling Optimization Prompt

Use this prompt to improve error handling in your code:

```
I need to improve the error handling in this code. Please help me by:

1. Identifying places where errors might occur
2. Adding appropriate try/catch blocks
3. Creating specific error types/messages where needed
4. Ensuring resources are properly cleaned up
5. Adding logging for errors
6. Following error handling best practices for [LANGUAGE/FRAMEWORK]

Here's the code:

[PASTE YOUR CODE HERE]
```

## Performance Optimization Prompt

Use this prompt to improve code performance:

```
Please help me optimize this code for better performance by:

1. Identifying performance bottlenecks
2. Suggesting more efficient algorithms or data structures
3. Reducing unnecessary computations or memory usage
4. Considering time and space complexity
5. Suggesting potential parallelization opportunities
6. Maintaining readability while improving efficiency

Here's the code:

[PASTE YOUR CODE HERE]
```

## How to Use These Prompts

1. Copy the appropriate prompt based on your optimization needs
2. Replace `[PASTE YOUR CODE HERE]` with the code you want to optimize
3. Replace `[LANGUAGE/FRAMEWORK]` with your specific language or framework (e.g., Python, JavaScript, React)
4. Submit the prompt to GitHub Copilot or Edge Copilot
5. Review the suggestions and implement the ones that make sense for your codebase

These prompts are designed to guide the AI to provide more targeted and useful optimization suggestions. Feel free to modify them to better suit your specific needs.
