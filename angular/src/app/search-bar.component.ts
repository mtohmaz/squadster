import { Component, ViewEncapsulation, OnInit } from "@angular/core";
import { DropdownModule } from "ng2-bootstrap/ng2-bootstrap";
import { Headers, Http, Response } from '@angular/http';

@Component({
    selector: 'searchbar',
    templateUrl: 'html/search-bar.component.html',
    encapsulation: ViewEncapsulation.None,
    styleUrls: ['styles/search-bar.component.css'],
})

export class SearchBarComponent {
    
    private headers = new Headers({'Content-Type': 'application/json'});
    
    constructor(private http: Http) {}
    
    public status:{isopen:boolean} = {isopen: false};
    distances = ['1 mile', '5 miles', '10 miles', '15 miles'];
    tags = ['Food', 'Gaming', 'Hangout', 'Movie', 'Sports', 'Study'];
    locations = ['Current Location', 'Raleigh, NC', 'Cary, NC', 'Durham, NC', 'Chapel Hill, NC'];
    distanceSelected = this.distances[0];
    tagSelected = null;
    locationSelected = this.locations[0];
    searchString = '';

    testPrint(){
        console.log('Now searching for: \n search string: ' + this.searchString + ' tag selected: ' + this.tagSelected + ', distance: ' + this.distanceSelected + ', location selected: ' + this.locationSelected);
    }

    updateSearch( search: string ){
        this.searchString = search;
        this.testPrint();
    }
    
    public doLogout():void {
        console.log('made it to doLogout');
        return this.http
               .delete('http://localhost/api/auth/', null, {headers: this.headers})
               .toPromise()
               .then(response => console.log(response.json()))
               .catch(this.handleError);
    }

    updateTag( tag ){
        this.tagSelected = tag;
        this.testPrint();
    }
}
