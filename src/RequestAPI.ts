import axios, { type AxiosResponse } from "axios";
export const baseUrl: string = "http://127.0.0.1:8000/"; // This is provided with a backslash '/' at the end

// interface Params {
//     [index: string]: string;
// }
// let d = {};
export enum Rtype {
    background = "background",
    music = "music",
    character = "character",
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
    if (name.length < 4) throw new Error("project name must at least have 4 characters");
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `init_project/?base_dir=${name}`
            getUrl("init_project", { base_dir: name })
        );
        // console.log(response.data.content["task_id"]);
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
export async function getResources(id: string, rtype: Rtype): Promise<Array<string>> {
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
export async function uploadFiles(id: string, rtype: string, formData: FormData): Promise<boolean> {
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
    let project_names: string[];
    try {
        // fetch the name
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("list_projects", {})
        );
        project_names = response.data.content;
        return project_names;
    } catch (err: any) {
        throw new Error("error happend in getProject");
        return project_names;
    }
    return project_names;
}

/**
 * delete a projet that has initilized before
 * @param id
 * @returns true if success, false if failed
 */
export async function removeProject(id: string): Promise<boolean> {
    //TO TEST;
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("remove_project", { task_id: id })
        );
        console.log(response);
        return response.data["status"] === 1;
    } catch (err: any) {
        throw new Error("error happend in removeProject");
        return false;
    }
    return false;
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
        return false;
    }
    return false;
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
        return false;
    }
    return false;
}
