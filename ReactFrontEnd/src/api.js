import axios from "axios";

// Configure axios to use the backend URL
const API_BASE_URL = "http://127.0.0.1:5000";

/**
 * POST /clean
 * @param {File} file CSV file object
 * @returns {Promise<Array>} cleaned preview rows
 */
export const cleanCsv = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await axios.post(`${API_BASE_URL}/clean`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data; 
};

/**
 * POST /forecast
 * @param {Array} rows full cleaned ds/y rows
 * @returns {Promise<{forecast:Array,low_confidence:boolean}>}
 */
export const forecast = async (rows) => {
  const { data } = await axios.post(`${API_BASE_URL}/forecast`, { data: rows });
  return data;
};