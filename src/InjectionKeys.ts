import type { InjectionKey, Ref } from "vue";
import type { EditorElement } from "./FrameDef";
export const hostNameKey = Symbol() as InjectionKey<string>;
export const projectIDKey = Symbol() as InjectionKey<Ref<string | undefined>>;
export const projectNameKey = Symbol() as InjectionKey<Ref<string | undefined>>;
export const editorElementsKey = Symbol() as InjectionKey<Array<EditorElement>>;
