# Animo

## What is Animo?

Animo is a Python package that allows you to create animations from text using Manim under the hood.

## Installation

```bash
pip install animo
```

## Usage

```python
from animo import Animo

client = Animo(api_key="your_api_key")

# Create a single video
code = """
class GenScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.play(Create(circle))
"""

response = client.videos.create(
    code=code,
    file_class="GenScene",
    aspect_ratio="16:9"
)

# Response format
response = {
    "message": "Video generation completed",
    "video_url": "https://animovideo.blob.core.windows.net/animocontainer/video-xxx.mp4"
}

# Export multiple scenes
scenes = [
    {"videoUrl": "https://animovideo.blob.core.windows.net/animocontainer/scene1.mp4"},
    {"videoUrl": "https://animovideo.blob.core.windows.net/animocontainer/scene2.mp4"}
]

export_response = client.videos.export(
    scenes=scenes,
    title_slug="my-animation"
)
```

## Development

### Requirements
- Python 3.9.6 or later
- Poetry (recommended for dependency management)

### Setup for Development

1. Clone the repository
```bash
git clone https://github.com/marcelo-earth/generative-manim.git
cd generative-manim/animo
```

2. Install dependencies
```bash
poetry install
```

### TODO
- [ ] Add unit tests using pytest
- [ ] Add more examples
- [ ] Add documentation
- [ ] Add CI/CD pipeline

## License

[MIT License](LICENSE)
