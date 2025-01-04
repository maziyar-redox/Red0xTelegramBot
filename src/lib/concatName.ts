export default function ConcatName(firsName: string | undefined, lastName: string | undefined): string {
    const FirstName = `${typeof(firsName) === "string" ? firsName : ""}`;
    const LastName = `${typeof(lastName) === "string" ? lastName : ""}`;
    let ConcatName = "";
    if (FirstName.length !== 0 && LastName.length !== 0) {
        ConcatName = FirstName + " " + LastName;
    };
    if (FirstName.length === 0) {
        ConcatName = LastName;
    };
    if (LastName.length === 0) {
        ConcatName = FirstName;
    };
    return ConcatName;
};