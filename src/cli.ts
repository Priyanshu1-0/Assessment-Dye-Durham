import { NameSorterApp } from './app/NameSorterApp.ts';
import { byLastNameThenGivenNames } from './domain/NameOrdering.ts';
import { NameSorter } from './domain/NameSorter.ts';
import { CompositeNameSink } from './io/CompositeNameSink.ts';
import { ConsoleNameSink, type TextOutput } from './io/ConsoleNameSink.ts';
import { FileNameSink } from './io/FileNameSink.ts';
import { FileNameSource } from './io/FileNameSource.ts';

/** The sorted names are always written here, relative to the working directory. */
export const OUTPUT_FILE_NAME = 'sorted-names-list.txt';

export const USAGE = `Usage: name-sorter <path-to-unsorted-names-list>

Sorts the names in the given file by last name, then by given names.
The result is printed to the screen and written to ./${OUTPUT_FILE_NAME}.`;

/** Where the CLI should print to; defaults to the real process streams. */
export interface CliStreams {
  stdout: TextOutput;
  stderr: TextOutput;
}

/**
 * The composition root: turns command-line arguments into a configured
 * `NameSorterApp`, runs it, and translates the outcome into an exit code.
 *
 * @param args command-line arguments, excluding the node binary and script path.
 * @returns the process exit code: 0 on success, 1 on any failure.
 */
export async function runCli(
  args: readonly string[],
  streams: CliStreams = { stdout: process.stdout, stderr: process.stderr },
): Promise<number> {
  const [inputFilePath, ...unexpectedArgs] = args;

  if (inputFilePath === undefined || unexpectedArgs.length > 0) {
    streams.stderr.write(`${USAGE}\n`);
    return 1;
  }

  const app = new NameSorterApp(
    new FileNameSource(inputFilePath),
    new NameSorter(byLastNameThenGivenNames),
    new CompositeNameSink([new ConsoleNameSink(streams.stdout), new FileNameSink(OUTPUT_FILE_NAME)]),
  );

  try {
    await app.run();
    return 0;
  } catch (error) {
    streams.stderr.write(`Error: ${describe(error)}\n`);
    return 1;
  }
}

function describe(error: unknown): string {
  return error instanceof Error ? error.message : String(error);
}
