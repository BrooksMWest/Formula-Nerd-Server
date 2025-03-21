

## Formula Nerd API
This API enables developers to maintain a database which keeps track of many of the important facets of Formula 1 racing. It manages non-user specific data, including drivers, constructors, racing circuits, and the Grands Prix (races) that take place at those circuits all over the world. It also allows users to see the histories between drivers and constructors. 

Let's drive! 

### Setup

1. Clone the template repository.
2. Navigate to the created directory using `cd`.
3. Activate the Pipenv environment with `pipenv shell`.
4. Install the dependencies using `pipenv install`.
5. Open the project in Visual Studio Code.
6. Ensure that the correct interpreter is selected.
7. Implement the code.

### MVP Routes by Entity Documentation

Documentation in Postman https://documenter.getpostman.com/view/29418828/2sAYk7S4Qf

This repository includes tests that you can use to assess your code against the MVP (Minimum Viable Product) requirements. You can run these tests by following the instructions below:

### Using `python manage.py test`

1. Open your terminal or command prompt.
2. Navigate to the project's root directory.
3. Run the following command to execute the tests:

   ```bash
   python manage.py test
   ```

4. The results of the tests will be displayed in the terminal. Use your debugging skills to interpret the test results.
5. If you have any questions or encounter issues with the tests, feel free to create a discussion ticket to seek help and clarification.

### Using `pytest` (Note: VSCode Compatibility)

We have also set up pytest for testing purposes. However, please be aware that there might be compatibility issues with VSCode that could prevent pytest from working correctly. If you encounter any problems with pytest, please follow the steps below:

1. Attempt to run the tests using pytest by running the following command:

   ```bash
   pytest
   ```

2. If pytest works as expected, you can use it for testing. However, if you encounter any issues, follow the alternative method using `python manage.py test` as described above.

By following these instructions, you can effectively test your code against the MVP requirements and seek assistance if needed.

## Viewing Test Results on GitHub

To check the results of your tests on GitHub within your Pull Request (PR), follow these steps:

1. **Create Your Pull Request (PR)**: After completing your assignment, submit it by creating a PR. Ensure that your changes are pushed to your repository.
2. **Visit the Pull Request Page**: Go to your GitHub repository and click on the "Pull Requests" tab. You should find your PR listed there.
3. **Check the "Checks" Section**: Open your PR and scroll down to the section that either says "All checks have failed" or "All checks have passed."
4. **Expand the Checks**: If the checks are not already open, click on "show all checks" to reveal the details.
5. **Locate "GitHub Classroom Workflow"**: Among the checks, find the one labeled "GitHub Classroom Workflow." Click on the "Details" button next to it.
6. **Navigate to the Autograding Log**: You'll be taken to a details view. Look for the log with "Autograding" in the title, and expand it to reveal more information.
7. **Inspect the Test Session**: Scroll down within the expanded autograding log until you find the line that says "test session starts." From this point, you'll see a list of tests that either failed or succeeded.
8. **Review Test Results**: Carefully review the test results to determine which tests passed and which ones failed. This information will help you assess the status of your code.
9. **Act on Test Failures**: If any tests failed, use the information provided to understand the issues and make the necessary code adjustments. Remember that you can push new changes to your branch to trigger another test run.
10. **Merge Your PR**: Once all tests pass, and you are satisfied with your code, proceed to merge your PR into the main branch.

By following these detailed steps, you'll be able to access and interpret the test results within your GitHub PR, making it easier to address any issues and ensure the successful submission of your assignment.

## Submitting Your Assignment

Here's how you can officially submit your assignment and complete the assessment:

1. **Confirm Passing Tests**: Before proceeding, ensure that all the tests pass on your PR. You can check this following the steps in the Viewing Test Results on GitHub section above.
2. **Merge into Main**: If all tests pass successfully, merge your PR into the main branch. This indicates that your code meets the MVP requirements and is ready for assessment.
3. **Instructor Review**: Your instructor will carefully review your repo, assessing your code based on the project requirements, guidelines, and test runs.
4. **Wait for Instructor Feedback**: Once your instructor has reviewed your code, they may provide feedback or let you know that your code meets the requirements. This feedback may come through direct messages (DMs) or celebratory messages on Slack, depending on your class's communication method.
5. **Assignment Completion**: Your assignment is considered complete when the following conditions are met:
   - All tests pass on the main branch.
   - Your instructor has given you the thumbs up or indicated your code meets the requirements.
6. **Follow Additional Instructions**: If your instructor provides any further instructions or asks for revisions, be sure to follow their guidance.

By following these steps, you'll be able to confidently submit your assignment, receive feedback from your instructor, and successfully complete the assessment process.

## Seeking Help and Clarification

If you encounter challenges or need clarification during the assessment, follow these steps:

1. Create a new discussion ticket in the [GitHub Discussions](https://github.com/orgs/nss-evening-web-development/discussions) repository, providing all the necessary details about your issue or question.
2. Include a clear and concise description of the problem, along with any relevant code snippets, error messages, or logs.
3. Specify the context of the problem, including the route or feature you are working on and any relevant dependencies.
4. Once you have created the discussion ticket, post a link to it in the Help Thread within your cohort's designated communication channel (e.g., Slack).
5. Be patient and allow time for the instructional team to review and respond to your ticket. They will provide guidance or clarification to help you move forward.

By following these steps, you can ensure that your questions and issues are properly documented and brought to the attention of the instructional team. This process helps streamline communication and allows the team to provide timely and targeted assistance to support your progress during the assessment.
