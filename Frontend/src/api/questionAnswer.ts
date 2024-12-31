import service from "@/utils/request";

export function getMeta(id: string | number) {
    return service({
        url: '/meta',
        method: 'get',
        params:id
    })
}

export function getQAs(id: string | number) {
    return service({
        url: '/qa',
        method: 'get',
        params:id
    })
}