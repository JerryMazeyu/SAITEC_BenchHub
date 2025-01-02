import service from "@/utils/request";

export function getAllPapers() {
    return service({
        url: '/papers',
        method: 'get',
    })
}