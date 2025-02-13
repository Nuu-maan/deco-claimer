# Decoration Claimer & Equipper

## Overview

This script automates the process of claiming and equipping decorations for a specified set of accounts. It supports proxy usage to avoid detection and rate limits.

## Features

- Automatically claims decorations
- Equips claimed decorations
- Supports rotating proxies
- Multi-account support
- Logging for better debugging

## Requirements

- Python 3.10+
- `requests` library
- A valid proxy list (Iproyal recommended)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Nuu-maan/deco-claimer.git
   cd deco-claimer
   ```

2. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare input files:**

   - Place your tokens inside `input/tokens.txt` (one per line)
   - Place your proxies inside `input/proxies.txt` using this format:
     ```
     http://username:password@host:port
     ```

## Usage

Run the script with:

```sh
python main.py
```

### Expected Output

```bash
Starting Decoration Claimer & Equipper...
Trying proxy: http://yourproxy@host:port
[✓] Successfully claimed decoration ▸ token=xxxxxxx
```

## Troubleshooting

- **Proxy errors?** Ensure your proxies are formatted correctly.
- **Failed claims?** Some decorations might already be claimed or unavailable.
- **Script crashes?** Check `logs/errors.log` for details.

## Contributing

Pull requests are welcome. Feel free to open issues for bug reports or feature requests.

## License

MIT License. See `LICENSE` for details.
