export class User {
    /**
     * User data structure
     *
     */

    constructor(username = "default", breakTime = 0, workTime = 0) {
        this.username = username;
        this.breakTime = breakTime; //seconds
        this.workTime = workTime; //seconds

        this.notes = [
            {
              name: "english",
              notes: [
                "the mitochondria is the powerhouse of the cell",
                "hank green whooo",
                "more random notes",
              ],
            },
            {
              name: "math",
              notes: [
                "1 + 1 = 2",
                "2 + 2 = 4",
                "math is fun!",
              ],
            },
        ]
        console.log("created!")
    }

    getUserName() {
        return this.username;
    }

    getBreakTime() {
        return this.breakTime;
    }

    getWorkTime() {
        return this.workTime;
    }

    getNotes() {
        return this.notes;
    }

    setUserName(username) {
        this.username = username;
    }

    setTime(time_info) {
        this.workTime = Number(time_info.work.mins) * 60 + Number(time_info.work.secs);
        this.breakTime = Number(time_info.break.mins) * 60 + Number(time_info.break.secs);
    }

    setNotes(notes) {
        this.notes = notes;
    }
}