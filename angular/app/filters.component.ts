import {Component, ViewEncapsulation, OnInit} from "@angular/core";
//import {Routes} from "./../../config/route.config";
@Component({
    selector: "filters",
    templateUrl: 'app/html/filters.component.html',
    styleUrls: ['app/styles/filters.component.css']
})

export class FiltersComponent {
    public checkModel:any = {food: false, sports: false, hangout: false, movie: false, study: false, gaming: false};
    public minDate: Date = void 0;
    constructor()
    {
        (this.minDate = new Date()).setDate(this.minDate.getDate());
    }
}
