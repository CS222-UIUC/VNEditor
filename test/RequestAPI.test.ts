import { getUrl, baseUrl, initProject, getResources, Rtype } from "../src/RequestAPI";
import { test, describe, expect } from "vitest";
import { assert } from "console";

describe("getUrl", () => {
    test("empty api string should throw", () => {
        expect(() => getUrl("", { a: "abc" })).toThrowError();
    });

    test("empty params should work", () => {
        expect(getUrl("test", {})).toBe(baseUrl + "test/");
    });

    test("single param", () => {
        expect(getUrl("test", { a: "abc" })).toBe(baseUrl + "test/?a=abc");
    });

    test("multiple params", () => {
        expect(getUrl("test", { a: "abc", b: "123", c: "xyz098" })).toBe(
            baseUrl + "test/?a=abc&b=123&c=xyz098"
        );
    });

    test("param with numbers", () => {
        expect(getUrl("test", { a: 12345 })).toBe(baseUrl + "test/?a=12345");
    });
});

describe("initProject", () => {
    test("empty string should throw", async () => {
        await expect(initProject("")).rejects.toThrowError();
    });

    test("the same name should return the same id", async () => {
        const r1 = await initProject("test1");
        const r2 = await initProject("test1");
        expect(r1).toBe(r2);
    });

    test("different name should return the different id", async () => {
        const r1 = await initProject("test1");
        const r2 = await initProject("test2");
        expect(r1).not.toBe(r2);
    });
});

describe("getResources", () => {
    test("empty resources on init", () => {
        initProject("some-unused-name").then(async (id?: string) => {
            expect(id).toBeDefined();
            if (id) {
                expect(await getResources(id, Rtype.background)).toBe([]);
                expect(await getResources(id, Rtype.music)).toBe([]);
                expect(await getResources(id, Rtype.character)).toBe([]);
            }
        });
    });
});

describe("removeProject", () => {
    test("empty resources on init", () => {});
});

describe("getProjects", () => {
    test("empty resources on init", () => {});
});

describe("getProjects", () => {
    test("empty resources on init", () => {});
});
