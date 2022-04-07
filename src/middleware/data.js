export class User {
    /**
     * User data structure
     * 
     */

    constructor(username = "default", breakTime = "1201", workTime = "1220", notes ={}) {
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

    setBreakTime(breakTime) {
        this.breakTime = breakTime;
    }

    setWorkTime(workTime) {
        this.workTime = workTime;
    }

    setNotes(notes) {
        this.notes = notes;
    }
}