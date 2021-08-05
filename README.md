# issue-mapper

The repo demonstrates how you can use GitHub Actions to fetch a map and insert it into a issue comment.

## Usage

Create an issue in this repo using the issue template. Input numeric values for latitude and longitude, create the issue, wait a few seconds for the action to complete, and you should see a new automatically generated comment in the issue containing a map centered on the coordinates.

## Why?

I don't have a great reason for making this repo, other than to explore GitHub Actions.

If you really want a png map, you should go to the [Mapbox Static Images API Playground](https://docs.mapbox.com/playground/static/). You can make maps faster and with your own API key there.

## Known Limitations

This repo does some things really poorly.

- each time a map is created, it goes into the `/images` folder. Not only does this pollute the commit history, it counts against the repo size limit. There should be room for a few thousand small maps, but eventually I'll need a solution to securely store and access maps in the cloud, or delete old map commits and files from the git history. Anyway, please don't try to automatically generate thousands of maps.
