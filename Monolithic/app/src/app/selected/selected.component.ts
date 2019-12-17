import { Component, OnInit,ChangeDetectionStrategy,ChangeDetectorRef } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {  Router  } from '@angular/router';
@Component({
  selector: 'app-selected',
  templateUrl: './selected.component.html',
  styleUrls: ['./selected.component.css'],
  changeDetection : ChangeDetectionStrategy.Default
})
export class SelectedComponent implements OnInit {
  private data : any = []
  showLoadingIndicator;
  constructor(private http: HttpClient ,private cd: ChangeDetectorRef) {}
 
  getData(){
    this.showLoadingIndicator = true;
    const url ='http://127.0.0.1:5000/clusterlabel'
    this.http.get(url).subscribe((res)=>{
      this.data = res
      this.showLoadingIndicator = false;
      this.cd.detectChanges();   
    });
  }
  ngOnInit() {
   this.getData()
 }
}
