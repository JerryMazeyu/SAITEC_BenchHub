import service from "@/utils/request";

export function getAllBenchMarks() {
    return service({
        url: '/benchmarks/dimensions',
        method: 'get',
    })
}