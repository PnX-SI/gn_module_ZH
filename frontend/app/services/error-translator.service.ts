import { Injectable } from "@angular/core";

type error = {
  api: string;
  front: string;
};

@Injectable({
  providedIn: "root",
})
export class ErrorTranslatorService {
  constructor() {}

  private errors = [
    {
      api: "400 Bad Request: polygon_contained_in_zh", // error returned by backend
      front: "La geometrie est contenue entièrement dans une autre zone humide", //error to show to the user
    },
    {
      api: "ZH_main_name_already_exists", // error returned by backend
      front:
        "Impossible de créer un identifiant unique avec les informations entrées. Le nom est peut-être déjà pris ?", //error to show to the user
    },
  ];

  getFrontError(errorMsg: string): string {
    console.log("error:", errorMsg);
    const frontError: error = this.errors.filter(
      (item) => item.api == errorMsg
    )[0];
    console.log(frontError);
    return frontError ? frontError.front : "Erreur inconnue";
  }
}
