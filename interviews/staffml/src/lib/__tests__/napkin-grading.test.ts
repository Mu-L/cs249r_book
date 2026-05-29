import { describe, expect, test } from "vitest";
import { checkNapkinMath, extractFinalNumber } from "../corpus";

describe("checkNapkinMath — sub-unit answers (Bug 3)", () => {
  test("a 2x miss on a sub-unit answer is NOT graded 'within tolerance'", () => {
    // model 0.5, user 1.0 → true relative error 100%. The old code divided by
    // max(0.5,1)=1, scoring ratio 0.5 → "ballpark". With |model| it is 1.0.
    const r = checkNapkinMath(1.0, 0.5, "cloud");
    expect(r.ratio).toBeCloseTo(1.0, 5);
    expect(r.grade).toBe("ballpark"); // ratio <= 1.0 boundary, but no longer "close"
    expect(["exact", "close"]).not.toContain(r.grade);
  });

  test("exact match on a sub-unit answer grades 'exact'", () => {
    const r = checkNapkinMath(0.5, 0.5, "cloud");
    expect(r.ratio).toBe(0);
    expect(r.grade).toBe("exact");
  });

  test("within-tolerance on a sub-unit answer still grades 'close' or better", () => {
    // cloud tolerance 0.25; 0.55 vs 0.5 → 10% error → within tolerance.
    const r = checkNapkinMath(0.55, 0.5, "cloud");
    expect(r.ratio).toBeCloseTo(0.1, 5);
    expect(["exact", "close"]).toContain(r.grade);
  });

  test("large-magnitude answers keep working", () => {
    const r = checkNapkinMath(1_050_000, 1_000_000, "cloud");
    expect(r.ratio).toBeCloseTo(0.05, 5);
    expect(["exact", "close"]).toContain(r.grade);
  });

  test("model answer of 0: nonzero guess is way off with a finite label", () => {
    const r = checkNapkinMath(5, 0, "cloud");
    expect(r.grade).toBe("way_off");
    expect(r.label).toBe("Way off"); // not "Off by Infinity×"
  });

  test("model answer of 0 and user 0 is exact", () => {
    const r = checkNapkinMath(0, 0, "cloud");
    expect(r.grade).toBe("exact");
  });
});

describe("extractFinalNumber — garbage rejection (Bug 4)", () => {
  test("a lone comma does NOT parse to 0", () => {
    expect(extractFinalNumber(",")).toBeNull();
    expect(extractFinalNumber("the cache, the model, the data")).toBeNull();
  });

  test("returns the last numeric token", () => {
    expect(extractFinalNumber("first 12 then 34")).toBe(34);
  });

  test("strips thousands separators", () => {
    expect(extractFinalNumber("about 1,024 GB")).toBe(1024);
  });

  test("honors an explicit answer marker", () => {
    expect(extractFinalNumber("scratch work 99\nanswer: 42")).toBe(42);
    expect(extractFinalNumber("=> 3.5")).toBe(3.5);
  });

  test("a marker with no digit falls through instead of yielding 0", () => {
    expect(extractFinalNumber("answer: ,")).toBeNull();
  });

  test("a hyphen range reads as the trailing positive number, not a negative", () => {
    expect(extractFinalNumber("10-20 ms")).toBe(20);
  });

  test("decimals survive", () => {
    expect(extractFinalNumber("the result is 0.5 GB")).toBe(0.5);
  });
});
