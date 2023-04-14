export interface IChar {
    imageName: string;
    position: [number, number];
}

export interface IFrame {
    name: string; // name of the frame
    id: Number; // index
    backgroundName: string; // url
    characters: IChar[];
    branch?: IFrame[];
}
