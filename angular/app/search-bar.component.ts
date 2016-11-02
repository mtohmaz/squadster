import { Component, ViewEncapsulation, OnInit } from "@angular/core";
import { DropdownModule } from "ng2-bootstrap/ng2-bootstrap";

@Component({
    selector: 'searchbar',
    templateUrl: 'app/html/search-bar.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['app/styles/search-bar.component.css'],
})

export class SearchBarComponent {
    public status:{isopen:boolean} = {isopen: false};
    //public distances:Array<string> = ['1 mile', '5 miles', '10 miles', '15+ miles'];
    //public locations:Array<string> = ['Current location', 'Raleigh, NC', 'Cary, NC', 'Durham, NC', 'Chapel Hill, NC'];
    //public tags:Array<string> = ['Food', 'Gaming', 'Hangout', 'Movie', 'Sports', 'Study'];
    items = [{name: 'one'}, {name: 'two'}];
    distances = [{distance: '1 mile'}, {distance: '5 miles'}, {distance: '10 miles'}, {distance: '15+ miles'}];
    tags = [{tag: 'Food'}, {tag: 'Gaming'}, {tag: 'Hangout'}, {tag: 'Movie'}, {tag: 'Sports'}, {tag: 'Study'}];
    locations = [{location: 'Current Location'}, {location: 'Raleigh, NC'},
        {location: 'Cary, NC'}, {location: 'Durham, NC'},{location: 'Chapel Hill, NC'},]

    public toggled(open:boolean):void {
        console.log('Dropdown is now: ', open);
    }

    public toggleDropdown($event:MouseEvent):void {
        $event.preventDefault();
        $event.stopPropagation();
        this.status.isopen = !this.status.isopen;
    }
}
