import service from "../utils/request";

  export function deletePaper(id: string | number) {
    return service({
      url: '/paper',
      method: 'delete',
      params: id,
    });
  }


  export function getAllPapers() {
    return service({
        url: '/papers',
        method: 'get',
    })
}
