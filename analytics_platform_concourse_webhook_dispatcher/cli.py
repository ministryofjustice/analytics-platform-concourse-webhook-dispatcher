#!/usr/bin/env python
"""Console script for analytics_platform_concourse_webhook_dispatcher."""
import sys
from pprint import pprint

import click

from analytics_platform_concourse_webhook_dispatcher.server import serve, app


@click.command()
@click.argument('cmd', type=click.Choice(['server', 'config']))
def main(cmd):
    """Console script for analytics_platform_concourse_webhook_dispatcher."""
    if cmd == 'server':
        serve()
    elif cmd == 'config':
        pprint(app.config)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
