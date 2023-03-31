import type { InjectionKey, Ref } from "vue";

export const hostNameKey = Symbol() as InjectionKey<string>;
export const projectIDKey = Symbol() as InjectionKey<Ref<string | undefined>>;
export const projectNameKey = Symbol() as InjectionKey<Ref<string | undefined>>;
