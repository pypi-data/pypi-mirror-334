# talktollm

A Python utility for interacting with large language models (LLMs) through a command-line interface. It leverages image recognition to automate interactions with LLM web interfaces, enabling seamless conversations and task execution.

## Features

-   **Command-Line Interaction:** Provides a simple and intuitive command-line interface for interacting with LLMs.
-   **Automated Image Recognition:** Employs image recognition techniques to identify and interact with elements on the LLM interface, such as input fields and submit buttons.
-   **Multi-LLM Support:** Currently supports DeepSeek and Gemini, with the potential for expansion to other LLMs.
-   **Automated Conversations:** Facilitates automated conversations and task execution by simulating user interactions with the LLM interface.
-   **Image Support:** Allows sending images to the LLM, handling the image processing and clipboard operations.
- **Easy to use:** The package is very easy to set up and use.

## Core Functionality

The core function of `talktollm` is the `talkto(llm, prompt, imagedata=None, debug=False)` function. This function takes the following arguments:

-   `llm`: The name of the LLM to interact with (e.g., 'deepseek' or 'gemini').
-   `prompt`: The text prompt to send to the LLM.
-   `imagedata`: Optional image data to send to the LLM. This should be a list of base64 encoded strings representing the images.
-   `debug`: A boolean flag to enable debugging output.

The `talkto` function performs the following steps:

1.  Opens the LLM's website in a new browser tab.
2.  Finds the message input box using image recognition (optimisewait).
3.  If image data is provided, it iterates through the images, converts them to the correct format, and pastes them into the LLM input.
4.  Pastes the provided text prompt into the LLM input.
5.  Finds and clicks the 'run' button using image recognition.
6.  Waits for the LLM to finish processing (for Gemini, it waits for a 'done' indicator).
7.  Finds and clicks the 'copy' button using image recognition.
8.  Closes the browser tab.
9.  Retrieves the LLM's response from the clipboard.

## Image Handling

`talktollm` includes functionality for handling images to be sent to the LLMs.

- `set_clipboard_image(image_data, retries=3, delay=0.2)` is used to set the image to the clipboard. This function takes base64 encoded image data, decodes it, converts it to a bitmap, and places it on the clipboard.
- `set_image_path(llm, debug=False)` is used to determine where the image is on the users computer by using the `copy_images_to_temp` function.
- `copy_images_to_temp(llm, debug=False)`: Copies images used for image recognition to the temporary directory.

## Installation

This section provides instructions on how to install the `talktollm` package.

```
pip install talktollm
```

## Usage

This will start by trying to find the LLM in the top left of the primary monitor. Basic usage instructions and examples are presented here.


```
python
import talktollm
response = talktollm.talkto('gemini', 'Write a poem about cats.')
print(response)

# Example with image
# response = talktollm.talkto('gemini', 'Describe this image', imagedata=['data:image/png;base64,iVBOR...'])

```
## Dependencies

Lists the external libraries that `talktollm` depends on.

-   pywin32
-   pyautogui
-   pillow
-   optimisewait

## Contributing

Describes how others can contribute to the development of `talktollm`.

Pull requests are welcome! For significant changes, it's recommended to open an issue first to discuss the proposed modifications. This helps ensure that contributions align with the project's goals and maintain overall consistency.

## License

Specifies the license under which `talktollm` is distributed.

MIT
