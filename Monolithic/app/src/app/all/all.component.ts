import { Component, OnInit,ChangeDetectionStrategy,ChangeDetectorRef} from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { HttpHeaders } from '@angular/common/http';
import {  Router  } from '@angular/router';

@Component({
  selector: 'app-all',
  templateUrl: './all.component.html',
  styleUrls: ['./all.component.css'],
  changeDetection : ChangeDetectionStrategy.Default
})
export class AllComponent implements OnInit {
  showLoadingIndicator;
  
  private data : any = []

  constructor(private http: HttpClient ,private router: Router,private cd: ChangeDetectorRef) {} 
     
  headers = new HttpHeaders({'Content-Type': 'application/json','Access-Control-Allow-Origin': '*'});

 getData(){
   const url ='http://127.0.0.1:5000/'  
   this.showLoadingIndicator = true;
   this.http.get(url).subscribe((res)=>{
      this.data=res
      console.log("responsereceived",this.data)
      this.showLoadingIndicator = false;
      this.cd.detectChanges();   
  });
 }
 ngOnInit() {
    this.getData();
}

onSelect(selectedItem: any) {
  console.log("Selected item Id: ", selectedItem.cluster_value);
  this.http.post("http://127.0.0.1:5000/angtoflask",{
    "label":String(""+selectedItem.cluster_value)
    }).subscribe(
    data => {
      console.log("callback:          "+data)
      this.router.navigate(['/selected']);
    },
    error  => {
      console.log("Error", error);
      }
  );
}
}
