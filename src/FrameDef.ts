export enum ElementType {
    Image,
    Text,
}

export interface EditorElement {
    content: string;
    xCoord: number;
    yCoord: number;
    w: number;
    h: number;
    type: ElementType;
}

export class Character implements EditorElement {
    content: string = "https://freepngimg.com/thumb/anime/1-2-anime-picture.png";
    xCoord: number = 10;
    yCoord: number = 10;
    w: number = 100;
    h: number = 100;
    type: ElementType = ElementType.Image;
}

export class Diaglog implements EditorElement {
    xCoord: number = 10;
    yCoord: number = 10;
    content: string = "This is a dialog";
    w: number = 1000;
    h: number = 200;
    type: ElementType = ElementType.Text;
}

export class Frame {
    name: string = ""; // name of the frame
    id: Number | undefined = undefined; // index
    backgroundName: string = ""; // url
    elements: EditorElement[] = [];
    branch?: Frame[];
}

export class FrameBack {
    background: string = "";
    chara: string[] = [];
    chara_pos: { x: number; y: number }[] = [];
    music: string = "";
    music_signal: number = 1;
    dialog: string = "";
    dialog_character: string = "";
    name: string = "";
}

export interface IFrame_left {
    // used for display of list of chapters
    FrameName: string; // name of the frame
    ChapterName: string;
    ProjectId: string;
    id: Number; // frame id
}
