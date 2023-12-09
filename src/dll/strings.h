#pragma once


template <typename... Args>
std::string format(const std::string& fmt, Args... args)
{
    const auto len = std::snprintf(nullptr, 0, fmt.c_str(), args...);
    std::vector<char> buf(len + 1);
    std::snprintf(buf.data(), len + 1, fmt.c_str(), args...); // NOLINT(cert-err33-c)
    const auto str = std::string(buf.begin(), buf.end());

    return str.substr(0, len); // remove null-terminated string
}

inline std::vector<std::string> split(const std::string str, char terminator)
{
    std::vector<std::string> vec;
    std::stringstream ss{str};
    std::string buf;

    while (std::getline(ss, buf, terminator))
        vec.push_back(buf);

    return vec;
}
