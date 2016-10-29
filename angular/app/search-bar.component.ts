import { Component, ViewEncapsulation, OnInit } from "@angular/core";
import { DropdownModule } from "ng2-bootstrap/ng2-bootstrap";

@Component({
    selector: 'searchbar',
    templateUrl: 'app/html/search-bar.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['app/styles/search-bar.component.css'],
})

export class SearchBarComponent {
    public disabled:boolean = false;
    public status:{isopen:boolean} = {isopen: false};

    public toggled(open:boolean):void {
        console.log('Dropdown is now: ', open);
    }

    public toggleDropdown($event:MouseEvent):void {
        $event.preventDefault();
        $event.stopPropagation();
        this.status.isopen = !this.status.isopen;
    }
}
