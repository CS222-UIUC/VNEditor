import axios, { type AxiosResponse } from "axios";
const baseUrl: string = "http://127.0.0.1:8000/"; // This is provided with a backslash '/' at the end

// interface Params {
//     [index: string]: string;
// }
// let d = {};
export function getUrl(api: string, params: { [key: string]: string | number }): string {
    let url: string = `${baseUrl}${api}/?`;
    let i: number = 0;
    if (params) {
        const keys = Object.keys(params);
        keys.forEach((key: string) => {
            url += `${key}=${params[key]}`;
            if (i < keys.length - 1) url += "&";
            i++;
        });
    }
    return url;
}

export async function initProject(name: string): Promise<string | undefined> {
    let projectID: string;
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

export async function getResources(id: string, rtype: string): Promise<Array<string> | undefined> {
    try {
        const response: AxiosResponse = await axios.post(
            // baseUrl + `get_res/?task_id=${id}&rtype=${rtype}`
            getUrl("get_res", { task_id: id, rtype: rtype })
        );
        console.log(response.data.content);
        // projectID = response.data.content["task_id"];
        return response.data.content;
    } catch (err: any) {
        return undefined;
    }
}

export async function uploadFiles(id: string, rtype: string, formData: FormData): Promise<boolean> {
    try {
        const response = await axios({
            method: "post",
            url: getUrl("upload", { task_id: id, rtype: rtype }),
            data: formData,
            headers: { "Content-Type": "multipart/form-data" },
        });
        return response.data["status"] === 1;
    } catch (err: any) {
        return false;
    }
}
