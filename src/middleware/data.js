export class User {
    /**
     * User data structure
     *
     */

    constructor(username = "default", breakTime = 1201, workTime = 1220, notes ={}) {
        this.username = username;
        this.breakTime = breakTime; //seconds
        this.workTime = workTime; //seconds
        this.notes = notes;
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