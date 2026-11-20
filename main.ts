// The World Today — Friday 20 November 2026.
//
// The entry is the poster itself: entry.png is a newspaper front page of the
// day's world news, drawn at build time from poster.html. This program does
// not draw anything; it proves the shipped image is a whole, in-limits PNG
// and copies it byte for byte into the output directory. Two runs therefore
// write identical bytes. It uses only the Node standard library and never
// touches the network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

function loadImage(): Buffer {
  return readFileSync(new URL("./entry.png", import.meta.url));
}

function checkPng(image: Buffer): { width: number; height: number } {
  // Magic bytes 89 50 4E 47, then IHDR width/height at offsets 16 and 20.
  if (image.subarray(0, 4).toString("hex") !== "89504e47") {
    throw new Error("entry.png does not start with the PNG magic bytes");
  }
  const width = image.readUInt32BE(16);
  const height = image.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, over the ${MAX_SIDE}x${MAX_SIDE} cap`);
  }
  // A whole PNG ends with the 12-byte IEND chunk (length 0 + "IEND").
  const tail = image.subarray(image.length - 12);
  if (tail.readUInt32BE(0) !== 0 || tail.subarray(4, 8).toString("ascii") !== "IEND") {
    throw new Error("entry.png has no IEND chunk at its end: not a whole PNG");
  }
  console.log(`poster is a whole ${width}x${height} PNG`);
  return { width, height };
}

function main(): void {
  const image = loadImage();
  if (image.length > MAX_BYTES) {
    throw new Error(`entry.png is ${image.length} bytes, over the 1 MiB cap`);
  }
  const { width, height } = checkPng(image);
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  writeFileSync(dest, image);
  console.log(`wrote ${dest} (${width}x${height}, ${image.length} bytes)`);
}

main();
