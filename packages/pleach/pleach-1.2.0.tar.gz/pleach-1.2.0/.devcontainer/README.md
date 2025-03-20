# Pleach Demo Codespace Readme

These instructions will walk you through the process of running a Pleach demo via GitHub Codespaces.

If you want a faster and easier demo experience with Pleach, DataStax Pleach is a hosted environment with zero setup: [Sign up for a free account.](https://astra.datastax.com/signup?type=pleach)

## Create a Codespace in GitHub

To setup the demo in Codespace:

1. Navigate to the Pleach repo
2. On the "Code <>" button, select the "Codespaces" tab
3. Click the green "Create codespace on..." button (or "+" icon if you want more options) to create a new Codespace

## Wait for everything to install

After the codespace is opened, there will be two phases to the process. It will take ≈5-10 minutes to complete.

* **Phase 1**: Building Container; you can click on the "Building Codespace" link to watch the logs
* **Phase 2**: Building Pleach; the terminal will now show `Running postCreateCommand...`, similar to:

```
✔ Finishing up...
⠸ Running postCreateCommand...
  › sudo chown -R pleach .venv .mypy_cache src/frontend/node_modules src/frontend/build src/backend/base/pleach/frontend && make install_frontend && mak…
```

Once completed, this terminal window will close.

You now need to manually build the frontend. Open a new Terminal and run command:

```bash
make build_frontend
```

This will take a short period of time, you should have a message similar to `Building frontend static files` and the command will complete successfully. 

Installation is now complete.

## Start up the Service

Open a new Terminal, and type `uv run pleach run`.

The service will start, and you will may notice a dialog in the lower right indicating there is a port available to connect to. However, the service will not be ready until you see the welcome banner:

```
╭───────────────────────────────────────────────────────────────────╮
│ Welcome to ⛓ Pleach                                              │
│                                                                   │
│                                                                   │                
│                                                                   │
│ We collect anonymous usage data to improve Pleach.                │
│ You can opt-out by setting DO_NOT_TRACK=true in your environment. │
│                                                                   │
│ Access http://127.0.0.1:7860                                      │
╰───────────────────────────────────────────────────────────────────╯
```

At this point you can connect to the service via the port, or if the dialog is gone you can find the "Forwarded Address" on the "Ports" tab (which is next the "Terminal" tab). If there is no port forwarded, you can click the "Forward a Port" button on the "Ports" tab, and forward `7860`. 