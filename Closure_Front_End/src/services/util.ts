import { AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";


/**
 * Similar to axios 'get', but works with Django's paginated responses,
 * yielding all available elements for the query.
 * 
 * @param http Axios HTTP instance
 * @param url URL used for initial request
 * @param config Axios configuration used for initial request. 
 *               If you want 
 * @returns Array of payload objects, tupled with an array of response objects.
 */
export async function djangoPaginatedGet(http: AxiosInstance, url: string, config?: AxiosRequestConfig): Promise<[any[], AxiosResponse<any>[]]>
{
    const totalResults = []
    let res = await http.get(url, config)
    const totalResponses = [res]
    totalResults.push(...res.data.results)
    while (res.data.next) {
        res = await http.get(res.data.next)
        totalResponses.push(res)
        totalResults.push(...res.data.results)
    }
    return [totalResults, totalResponses]
}