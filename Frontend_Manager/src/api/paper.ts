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

interface PaperData {
  name: string,
  author: string,
  journal: string,
  abstract: string,
  class: string,
  file_url: string,
}

  export function addPaper(data:PaperData) {
  return service({
      url: '/papers',
      method: 'post',
      data:data
  })
}

export function getAllBenchMarks() {
  return service({
      url: '/benchmarks',
      method: 'get',
  })
}

