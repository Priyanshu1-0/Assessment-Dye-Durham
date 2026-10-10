#!/usr/bin/env node
// Thin executable wrapper; all behaviour lives in src/cli.ts.
import { runCli } from '../src/cli.ts';

process.exitCode = await runCli(process.argv.slice(2));
