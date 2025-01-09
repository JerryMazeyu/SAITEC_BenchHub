import service from "../utils/request";

export function getQAs(params: { page: number; page_size: number; data_dimension: string }) {
    return service({
        url: '/benchmarks/testcases',
        method: 'get',
        params: params,
    });
}