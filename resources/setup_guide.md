# Setup Guide for Copilot Experiment

This guide provides instructions for setting up and using both Edge Copilot and GitHub Copilot for the experiment.

## Edge Copilot Setup (Week 1)

Edge Copilot is Microsoft's AI assistant integrated into the Edge browser. Here's how to set it up and use it effectively:

### Setup Instructions

1. **Open Microsoft Edge**
   - Ensure you're using the latest version of Microsoft Edge
   - If needed, update your browser by going to `...` > `Settings` > `About Microsoft Edge`

2. **Access Edge Copilot**
   - Click the Copilot icon in the top-right corner of your browser window
   - Alternatively, use the keyboard shortcut `Ctrl+Shift+I` (Windows) or `Cmd+Shift+I` (Mac)

3. **Sign In**
   - Sign in with your Lloyds Banking Group Microsoft account if prompted
   - This ensures you have access to all available features

### Using Edge Copilot for Coding Tasks

1. **Providing Context**
   - Copy relevant code snippets from your IDE into the Copilot chat
   - Provide clear instructions about what you're trying to accomplish
   - Include any specific requirements or constraints

2. **Working with Character Limitations**
   - Edge Copilot has character limitations for inputs
   - For large code bases, break your requests into smaller, focused chunks
   - Reference previous parts of the conversation when building on earlier requests

3. **Workflow Tips**
   - Keep Edge open in a separate window next to your IDE for easy reference
   - Use split-screen to view both simultaneously if possible
   - Copy-paste code between Edge Copilot and your IDE as needed

4. **Tracking Context Switching**
   - Note each time you need to switch between Edge and your IDE
   - Record this in your metrics as it's an important comparison point

## GitHub Copilot Setup (Week 2)

GitHub Copilot is an AI pair programmer that integrates directly into your IDE. Here's how to set it up:

### Setup Instructions

1. **Install the GitHub Copilot Extension**
   - **For VS Code:**
     - Open VS Code
     - Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
     - Search for "GitHub Copilot"
     - Click "Install"
   
   - **For JetBrains IDEs (PyCharm, IntelliJ, etc.):**
     - Go to Settings/Preferences
     - Select Plugins
     - Search for "GitHub Copilot"
     - Click "Install"

2. **Sign In to GitHub**
   - After installation, you'll be prompted to sign in to GitHub
   - Use your GitHub account that has been granted Copilot access
   - Follow the authentication prompts to complete setup

3. **Verify Installation**
   - Open a code file in your IDE
   - Start typing a comment or function signature
   - GitHub Copilot should begin offering suggestions

### Using GitHub Copilot Effectively

1. **Inline Suggestions**
   - As you type, Copilot will offer gray text suggestions
   - Press Tab to accept a suggestion or continue typing to ignore it
   - Use arrow keys to navigate through multiple suggestions

2. **Generating Complete Functions**
   - Write a descriptive comment explaining what you want the function to do
   - Press Enter and Copilot will suggest an implementation
   - Example: `// Function to calculate the mean absolute error between two arrays`

3. **Working with Context**
   - Copilot uses surrounding code as context for its suggestions
   - It can understand patterns in your codebase
   - It works best when it can see related functions and imports

4. **Keyboard Shortcuts**
   - **VS Code:**
     - Accept suggestion: Tab
     - Reject suggestion: Esc
     - Show next suggestion: Alt+] or Option+]
     - Show previous suggestion: Alt+[ or Option+[
     - Trigger inline suggestion: Alt+\ or Option+\
   
   - **JetBrains:**
     - Accept suggestion: Tab
     - Reject suggestion: Esc
     - Show next suggestion: Alt+] or Option+]
     - Show previous suggestion: Alt+[ or Option+[

## RS Copilot Library Integration

When working with the RS Copilot library during the experiment:

1. **Understanding the Library**
   - Review the RS Copilot examples provided in the `rs-copilot-examples` directory
   - Familiarize yourself with the library's patterns and conventions

2. **Testing Tool Understanding**
   - Observe how well each tool understands and works with RS Copilot patterns
   - Note whether the tool can suggest code that follows RS Copilot conventions
   - Record specific examples of successes or failures in your feedback

## Metrics Recording

Remember to record your metrics for each task:

1. **Time Tracking**
   - Note your start and end times
   - Track any significant breaks
   - Record the total time spent on each task

2. **Interaction Metrics**
   - Count the number of prompts/queries submitted
   - Note any character limitations encountered
   - Track context switching between tools and IDE

3. **Quality Assessment**
   - Evaluate the quality of the generated code or documentation
   - Assess how well the tool understood your requirements
   - Note any limitations or issues encountered

## Support

If you encounter any issues with setup or have questions during the experiment, please contact Hamza (experiment lead).
