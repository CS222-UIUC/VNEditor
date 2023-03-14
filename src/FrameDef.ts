export interface IChar {
    imageName: string;
    position: [number, number];
}

export interface IFrame {
    backgroundName: string; // url
    characters: IChar[];
    branch?: IFrame[];
}
