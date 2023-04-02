import axios, { type AxiosResponse } from "axios";
export const baseUrl: string = "http://127.0.0.1:8000/"; // This is provided with a backslash '/' at the end

import type { IFrame, IChar } from "@/FrameDef";
// interface Params {
//     [index: string]: string;
// }
// let d = {};
export enum Rtype {
    background = "background",
    music = "music",
    character = "character",
}
export enum Frametype {
    normal = "noraml", // normal frame, nothing special
    divergence = "divergence", // divergence frame, may apper choice , used for further development
}
/**
 *
 * @param api the name of api, would be attached to base_url
 * @param params the params as a key-value pairs
 * @returns return the generated url
 */
export function getUrl(api: string, params: { [key: string]: string | number }): string {
    if (api.length == 0) throw new Error("Expect non-empty api string but empty string is given");
    let url: string = `${baseUrl}${api}/`;
    let i: number = 0;
    if (params) {
        const keys = Object.keys(params);
        if (keys.length > 0) {
            url += "?";
            keys.forEach((key: string) => {
                url += `${key}=${params[key]}`;
                if (i < keys.length - 1) url += "&";
                i++;
            });
        }
    }
    return url;
}
/**
 * Initialize the project with the given name
 * @param name the name of the project to initialize. Must be more than 4 characters
 * @returns On success, return the project_id. Otherwise, return undefined
 */
export async function initProject(name: string): Promise<string | undefined> {
    let projectID: string;
    console.log(name);
    if (name.length < 4) throw new Error("project name must at least have 4 characters");
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `init_project/?base_dir=${name}`
            getUrl("init_project", { base_dir: name })
        );
        console.log(response.data.content["task_id"]);
        projectID = response.data.content["task_id"];
        return projectID;
    } catch (err: any) {
        return undefined;
    }
}
/**
 * The all the resources under the project of the given type
 * @param id project_id
 * @param rtype the enum class rtype. Should be one of "background" "music" "character"
 * @returns the list of names of the resources
 */
export async function getResources(id: string | undefined, rtype: Rtype): Promise<Array<string>> {
    if (!id) return [];
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("get_res", { task_id: id, rtype: rtype })
        );

        return response.data.content;
    } catch (err: any) {
        return [];
    }
}
/**
 *
 * @param id project id
 * @param rtype the enum class rtype. Should be one of "background" "music" "character"
 * @param formData FormData object containing files to be uploaded
 * @returns return true of upload is successful
 */
export async function uploadFiles(
    id: string | undefined,
    rtype: string,
    formData: FormData
): Promise<boolean> {
    if (!id) return false;

    try {
        const response = await axios({
            method: "post",
            url: getUrl("upload", { task_id: id, rtype: rtype }),
            data: formData,
            headers: { "Content-Type": "multipart/form-data" },
        });
        console.log(response);
        return response.data["status"] === 1;
    } catch (err: any) {
        return false;
    }
}
/**
 * return all the project name that user had initilized before
 * @param none
 * @returns return a list of string
 */
export async function getProjects(): Promise<string[]> {
    // TO TEST;
    try {
        // fetch the name
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("list_projects", {})
        );

        const project_names: string[] = response.data.content;
        return project_names;
    } catch (err: any) {
        console.log(err);
    }
    return [];
}

/**
 * delete a projet that has initilized before
 * @param name
 * @returns true if success, false if failed
 */
export async function removeProject(name: string): Promise<boolean> {
    //TO TEST;
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("remove_project", { project_name: name })
        );
        console.log(response);
        return response.data["status"] === 1;
    } catch (err: any) {
        throw new Error("error happend in removeProject");
    }
}
/**
 * delete a fioe that has uploaded before
 * @param id: project_id
 * @param rtype: the enum class rtype. Should be one of "background" "music" "character"
 * @param name: the file to be delete
 * @returns true if success, false otherwise
 */
export async function removeResource(id: string, rtype: Rtype, name: string): Promise<boolean> {
    // TO TEST
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("remove_res", { task_id: id, rtype: rtype, item_name: name })
        );
        console.log(response);
        return response.data["status"] === 1;
    } catch (err: any) {
        throw new Error("error happend in removeResource");
    }
}
/**
 * @param id: project_id
 * @param rtype: the enum class rtype. Should be one of "background" "music" "character"
 * @param old_name: the old file name to be changed
 * @param new_name: the new file name to be set
 * @returns
 */
export async function renameResource(
    id: string,
    rtype: Rtype,
    old_name: string,
    new_name: string
): Promise<boolean> {
    // TO TEST
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("rename_res", {
                task_id: id,
                rtype: rtype,
                item_name: old_name,
                new_name: new_name,
            })
        );
        console.log(response);
        return response.data["status"] === 1;
    } catch (err: any) {
        throw new Error("error happend in removeResource");
    }
}

/**
 * get all the chapters of the corresponding project
 * @param name: project_name
 * @returns
 */
export async function getChapters(name: string): Promise<string[]> {
    // need to update to correct function
    return ["test chapter", "next is chapter name", name, "end of chapter"];
}

/**
 * get all the frames of the corresponding chapter
 * @param name: project_name
 * @param chapter_name: chapter_name
 * @returns
 */
export async function getFrames(name: string, chapter_name: string): Promise<IFrame[]> {
    let a, c: IFrame;
    let b: IChar;
    b = {
        imageName: "",
        position: [0, 0],
    };
    a = {
        name: name, // name of the frame
        id: 0, // index
        backgroundName: "", // url
        characters: [b],
    };
    c = {
        name: chapter_name, // name of the frame
        id: 0, // index
        backgroundName: "", // url
        characters: [b],
    };
    return [a, c, a, a];
}
