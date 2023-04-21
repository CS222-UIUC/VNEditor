export interface EditorElement {
    imageUrl: string | undefined;
    xCoord: number;
    yCoord: number;
}

export class Character implements EditorElement {
    imageUrl: string = "https://freepngimg.com/thumb/anime/1-2-anime-picture.png";
    xCoord: number = 0.5;
    yCoord: number = 0.5;
}

export class Diaglog implements EditorElement {
    imageUrl: string | undefined = undefined;
    xCoord: number = 0.5;
    yCoord: number = 0.5;
    content: string = "";
}

export class Frame {
    name: string = ""; // name of the frame
    id: string = ""; // index
    backgroundName: string = ""; // url
    elements: EditorElement[] = [];
    branch?: Frame[];
}
