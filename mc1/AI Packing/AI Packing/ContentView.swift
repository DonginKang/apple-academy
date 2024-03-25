import SwiftUI


struct ResponseData {
    let essentialItems: [String]
    let weather: String
    let activities: [String]
    let toiletries: [String]
    let clothes: [String]
}

struct ChecklistView: View {
    let responseData: ResponseData
    
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("Essential Items")) {
                    ForEach(responseData.essentialItems, id: \.self) { item in
                        Text(item)
                    }
                }
                Section(header: Text("Weather")) {
                    Text(responseData.weather)
                }
                Section(header: Text("Activities")) {
                    ForEach(responseData.activities, id: \.self) { activity in
                        Text(activity)
                    }
                }
                Section(header: Text("Toiletries")) {
                    ForEach(responseData.toiletries, id: \.self) { toiletry in
                        Text(toiletry)
                    }
                }
                Section(header: Text("Clothes")) {
                    ForEach(responseData.clothes, id: \.self) { cloth in
                        Text(cloth)
                    }
                }
            }
            .navigationBarTitle("Checklist")
        }
    }
}


struct ContentView: View {
    @State private var items: String = ""
    @State private var gender: String = ""
    @State private var destination: String = ""
    @State private var startMonth: String = ""
    @State private var startDay: String = ""
    @State private var days: String = ""
    @State private var activities: String = ""
    @State private var responseData: ResponseData? = nil
    @State private var isShowingChecklist = false // ChecklistView를 표시할지 여부를 제어합니다.
    
    var body: some View {
        NavigationView { // NavigationView를 이곳으로 이동합니다.
            VStack {
                TextField("최소 체크리스트 개수 입력, 예: 10", text: $items)
                    .padding()
                    .keyboardType(.numberPad)
                TextField("성별 입력, 예: 남자", text: $gender)
                    .padding()
                TextField("목적지 입력, 예: 도쿄", text: $destination)
                    .padding()
                TextField("출발 월 입력, 예: 6", text: $startMonth)
                    .padding()
                    .keyboardType(.numberPad)
                TextField("출발 일 입력, 예: 10", text: $startDay)
                    .padding()
                    .keyboardType(.numberPad)
                TextField("여행 일수 입력, 예: 5", text: $days)
                    .padding()
                    .keyboardType(.numberPad)
                TextField("활동 입력, 예: 수영, 등산", text: $activities)
                    .padding()
                
                Button("Get Packs") {
                    getPacks(input_data: [
                        "items": items,
                        "gender": gender,
                        "destination": destination,
                        "start_month": startMonth,
                        "start_day": startDay,
                        "days": days,
                        "activities": activities
                    ])
                }
                .padding()
                
                // ChecklistView로 이동하는 버튼 추가
                Button("Show Checklist") {
                    self.isShowingChecklist = true
                }
                .padding()
            }
            .navigationBarTitle("Pack List Generator")
            .background( // VStack를 NavigationView의 하위에 위치시킵니다.
                NavigationLink(
                    destination: ChecklistView(responseData: responseData ?? ResponseData(essentialItems: [], weather: "", activities: [], toiletries: [], clothes: [])),
                    isActive: $isShowingChecklist,
                    label: { EmptyView() }
                )
                .hidden()
            )
        }
    }
    
    func getPacks(input_data: [String: String]) {
        let url = URL(string: "http://localhost:8080/basic")!
        
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
            
            if let httpResponse = response as? HTTPURLResponse {
                print("Status Code: \(httpResponse.statusCode)")
            }
            
            if let data = data {
                if let jsonResponse = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    print("Response Content: (jsonResponse)")
                    if let essentials = jsonResponse["필수 항목"] as? [String],
                       let weather = jsonResponse["날씨"] as? String,
                       let activities = jsonResponse["활동"] as? [String],
                       let toiletries = jsonResponse["세면 도구"] as? [String],
                       let clothes = jsonResponse["옷"] as? [String] {
                        let responseData = ResponseData(essentialItems: essentials,
                                                        weather: weather,
                                                        activities: activities,
                                                        toiletries: toiletries,
                                                        clothes: clothes)
                        print("Modified Response Data: (responseData)")
                        // 데이터를 설정하고 ChecklistView를 표시하기 위해 상태 변수를 업데이트합니다.
                        self.responseData = responseData
                        self.isShowingChecklist = true
                    }
                }
            }
        }
        task.resume()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
