// src/ app/ components/ ResultList.jsx

import styles from '../styles/ResultList.module.css';

export default function ResultList({ results }) {
  return (
    <ul className={styles.resultList}>
      {results.map((result, index) => (
        <tr key={index}>
          <td>{result['organism.scientificName']}</td>
        </tr>
      ))}
    </ul>
  );
}
