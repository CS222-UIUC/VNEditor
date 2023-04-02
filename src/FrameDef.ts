export interface IChar {
    imageName: string;
    position: [number, number];
}

export interface IFrame {
    id: string;
    backgroundName: string; // url
    characters: IChar[];
    branch?: IFrame[];
}
