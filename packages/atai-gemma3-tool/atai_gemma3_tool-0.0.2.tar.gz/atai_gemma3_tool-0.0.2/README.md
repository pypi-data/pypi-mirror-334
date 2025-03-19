# atai-gemma3-tool

atai-gemma3-tool is a command-line interface (CLI) tool that uses Google's Gemma 3 model to generate descriptive text from local image files. It leverages the power of a state-of-the-art multimodal model to process images and stream textual outputs in real time.

## Features

- **Multimodal Processing:** Accepts image input and produces text output.
- **Real-Time Streaming:** Generates and streams tokens as they are produced.
- **Customizable Prompt:** Allows users to define a custom prompt.
- **Easy Installation:** Installable via pip with all dependencies handled.
- **Asynchronous Generation:** Utilizes asynchronous token streaming for quick response times.

## Installation

Clone the repository and install the package in editable mode:

```bash
pip install git+https://github.com/huggingface/transformers@v4.49.0-Gemma-3

pip install atai-gemma3-tool
```

## Usage

Run the CLI tool from your terminal by specifying the path to your image file and an optional custom prompt:

```bash
atai-gemma3-tool "path/to/your/local_image.jpg" --prompt "Describe this image in detail."

atai-gemma3-tool https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/p-blog/candy.JPG
```

### Command Line Arguments

- **image_path**: The path to your local image file or a image url.
- **--prompt**: *(Optional)* Custom prompt for text generation.  
  Default: `"Describe this image in detail."`

The tool will load the image, process it using the Gemma 3 model, and output the generated text to your console in real time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **Google DeepMind:** For the Gemma 3 model.
- **Hugging Face:** For the Transformers library and supporting tools.
