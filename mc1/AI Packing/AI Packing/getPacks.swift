import Foundation

func getPacks(items: String, gender: String, destination: String, startMonth: String, startDay: String, days: String, activities: String, completion: @escaping ([String: [String]]) -> Void) {
    let url = URL(string: "http://localhost:8080/basic")!
    let input_data = [
        "items": items,
        "gender": gender,
        "destination": destination,
        "start_month": startMonth,
        "start_day": startDay,
        "days": days,
        "activities": activities
    ]

    guard let jsonData = try? JSONSerialization.data(withJSONObject: input_data) else {
        print("Error: Cannot create JSON data")
        return
    }

    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.httpBody = jsonData
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")

    let task = URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            print("Error: \(error)")
            return
        }

        if let data = data, let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: [String]] {
            DispatchQueue.main.async {
                completion(jsonResponse)
            }
        }
    }
    task.resume()
}
