import "@testing-library/jest-dom";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

afterEach(() => {
  cleanup();
});
/*
SOURCES / TEMPLATES USED:
- Testing Library jest-dom docs: `@testing-library/jest-dom` matchers
- Vitest integration docs: use `/vitest` entry to register matchers with Vitest
*/