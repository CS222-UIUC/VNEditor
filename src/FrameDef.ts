export interface EditorElement {
    imageUrl: string;
    xCoord: number;
    yCoord: number;
}

export class Character implements EditorElement {
    imageUrl: string = "https://freepngimg.com/thumb/anime/1-2-anime-picture.png";
    xCoord: number = 0;
    yCoord: number = 0;
}

export interface IFrame {
    name: string; // name of the frame
    id: Number; // index
    backgroundName: string; // url
    characters: Character[];
    branch?: IFrame[];
}
